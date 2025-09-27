"""Policy-driven configuration system for SafeLayer guardrails.

This module provides a flexible policy configuration framework that allows
dynamic guard configuration, rule-based enforcement, and policy inheritance.
"""

import json
import os
import yaml
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class PolicyAction(Enum):
    """Actions that can be taken when a guard is triggered."""
    BLOCK = "block"
    WARN = "warn"
    MASK = "mask"
    LOG_ONLY = "log_only"
    AUDIT = "audit"


class PolicySeverity(Enum):
    """Severity levels for policy violations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class GuardPolicy:
    """Configuration for a single guard."""
    guard_type: str
    enabled: bool = True
    action: PolicyAction = PolicyAction.BLOCK
    severity: PolicySeverity = PolicySeverity.MEDIUM
    threshold: float = 0.8
    custom_config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.custom_config is None:
            self.custom_config = {}


@dataclass
class PolicySet:
    """A collection of guard policies with metadata."""
    name: str
    version: str
    description: str
    guards: Dict[str, GuardPolicy]
    metadata: Dict[str, Any] = None
    parent_policy: Optional[str] = None  # For policy inheritance
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class PolicyManager:
    """Manages policy configuration and enforcement rules."""
    
    def __init__(self, config_dir: str = "./policies"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.loaded_policies: Dict[str, PolicySet] = {}
        self.active_policy: Optional[PolicySet] = None
        
        # Default policy fallback
        self._create_default_policy()
    
    def _create_default_policy(self) -> PolicySet:
        """Create a sensible default policy set."""
        default_guards = {
            "pii": GuardPolicy(
                guard_type="pii",
                enabled=True,
                action=PolicyAction.MASK,
                severity=PolicySeverity.HIGH,
                threshold=0.9
            ),
            "tone": GuardPolicy(
                guard_type="tone",
                enabled=True,
                action=PolicyAction.WARN,
                severity=PolicySeverity.MEDIUM,
                threshold=0.7
            ),
            "tts": GuardPolicy(
                guard_type="tts",
                enabled=True,
                action=PolicyAction.BLOCK,
                severity=PolicySeverity.CRITICAL,
                threshold=0.8
            )
        }
        
        default_policy = PolicySet(
            name="default",
            version="1.0.0",
            description="Default SafeLayer policy set",
            guards=default_guards,
            metadata={
                "created_by": "SafeLayer",
                "auto_generated": True
            }
        )
        
        self.loaded_policies["default"] = default_policy
        if self.active_policy is None:
            self.active_policy = default_policy
        
        return default_policy
    
    def load_policy(self, policy_file: Union[str, Path]) -> PolicySet:
        """Load a policy from file (JSON or YAML)."""
        policy_path = Path(policy_file)
        
        if not policy_path.exists():
            raise FileNotFoundError(f"Policy file not found: {policy_path}")
        
        with open(policy_path, 'r', encoding='utf-8') as f:
            if policy_path.suffix.lower() in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif policy_path.suffix.lower() == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported policy file format: {policy_path.suffix}")
        
        # Convert guard configurations to GuardPolicy objects
        guards = {}
        for guard_name, guard_config in data.get('guards', {}).items():
            guards[guard_name] = GuardPolicy(
                guard_type=guard_config.get('guard_type', guard_name),
                enabled=guard_config.get('enabled', True),
                action=PolicyAction(guard_config.get('action', 'block')),
                severity=PolicySeverity(guard_config.get('severity', 'medium')),
                threshold=guard_config.get('threshold', 0.8),
                custom_config=guard_config.get('custom_config', {})
            )
        
        policy = PolicySet(
            name=data.get('name', policy_path.stem),
            version=data.get('version', '1.0.0'),
            description=data.get('description', ''),
            guards=guards,
            metadata=data.get('metadata', {}),
            parent_policy=data.get('parent_policy')
        )
        
        # Handle policy inheritance
        if policy.parent_policy and policy.parent_policy in self.loaded_policies:
            policy = self._merge_policies(self.loaded_policies[policy.parent_policy], policy)
        
        self.loaded_policies[policy.name] = policy
        return policy
    
    def _merge_policies(self, parent: PolicySet, child: PolicySet) -> PolicySet:
        """Merge child policy with parent policy (child overrides parent)."""
        merged_guards = dict(parent.guards)
        merged_guards.update(child.guards)
        
        merged_metadata = dict(parent.metadata)
        merged_metadata.update(child.metadata)
        merged_metadata['inherited_from'] = parent.name
        
        return PolicySet(
            name=child.name,
            version=child.version,
            description=child.description,
            guards=merged_guards,
            metadata=merged_metadata,
            parent_policy=child.parent_policy
        )
    
    def save_policy(self, policy: PolicySet, filename: str = None) -> Path:
        """Save a policy to file."""
        if filename is None:
            filename = f"{policy.name}.yaml"
        
        filepath = self.config_dir / filename
        
        # Convert to serializable format
        policy_data = {
            'name': policy.name,
            'version': policy.version,
            'description': policy.description,
            'parent_policy': policy.parent_policy,
            'metadata': policy.metadata,
            'guards': {}
        }
        
        for guard_name, guard_policy in policy.guards.items():
            policy_data['guards'][guard_name] = {
                'guard_type': guard_policy.guard_type,
                'enabled': guard_policy.enabled,
                'action': guard_policy.action.value,
                'severity': guard_policy.severity.value,
                'threshold': guard_policy.threshold,
                'custom_config': guard_policy.custom_config
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(policy_data, f, default_flow_style=False, indent=2)
        
        return filepath
    
    def set_active_policy(self, policy_name: str) -> PolicySet:
        """Set the active policy by name."""
        if policy_name not in self.loaded_policies:
            raise ValueError(f"Policy not loaded: {policy_name}")
        
        self.active_policy = self.loaded_policies[policy_name]
        return self.active_policy
    
    def get_active_policy(self) -> PolicySet:
        """Get the currently active policy."""
        if self.active_policy is None:
            return self._create_default_policy()
        return self.active_policy
    
    def get_guard_config(self, guard_name: str) -> Optional[GuardPolicy]:
        """Get configuration for a specific guard."""
        active = self.get_active_policy()
        return active.guards.get(guard_name)
    
    def validate_policy(self, policy: PolicySet) -> List[str]:
        """Validate a policy configuration and return any issues."""
        issues = []
        
        if not policy.name:
            issues.append("Policy name is required")
        
        if not policy.version:
            issues.append("Policy version is required")
        
        for guard_name, guard_config in policy.guards.items():
            if not guard_config.guard_type:
                issues.append(f"Guard '{guard_name}' missing guard_type")
            
            if guard_config.threshold < 0 or guard_config.threshold > 1:
                issues.append(f"Guard '{guard_name}' threshold must be between 0 and 1")
        
        return issues
    
    def create_policy_template(self, name: str, guards: List[str]) -> PolicySet:
        """Create a policy template with specified guards."""
        template_guards = {}
        
        for guard_name in guards:
            template_guards[guard_name] = GuardPolicy(
                guard_type=guard_name,
                enabled=True,
                action=PolicyAction.BLOCK,
                severity=PolicySeverity.MEDIUM,
                threshold=0.8
            )
        
        return PolicySet(
            name=name,
            version="1.0.0",
            description=f"Template policy for {name}",
            guards=template_guards,
            metadata={
                "template": True,
                "created_by": "SafeLayer PolicyManager"
            }
        )
    
    def list_policies(self) -> List[str]:
        """List all loaded policy names."""
        return list(self.loaded_policies.keys())
    
    def get_policy_summary(self, policy_name: str) -> Dict[str, Any]:
        """Get a summary of a policy."""
        if policy_name not in self.loaded_policies:
            raise ValueError(f"Policy not found: {policy_name}")
        
        policy = self.loaded_policies[policy_name]
        return {
            'name': policy.name,
            'version': policy.version,
            'description': policy.description,
            'parent_policy': policy.parent_policy,
            'guard_count': len(policy.guards),
            'enabled_guards': len([g for g in policy.guards.values() if g.enabled]),
            'metadata': policy.metadata
        }


# Global policy manager instance
_policy_manager = None


def get_policy_manager() -> PolicyManager:
    """Get the global policy manager instance."""
    global _policy_manager
    if _policy_manager is None:
        # Check for environment variable to set config directory
        config_dir = os.getenv('SAFELAYER_POLICY_DIR', './policies')
        _policy_manager = PolicyManager(config_dir)
    return _policy_manager


def load_policy_from_env() -> Optional[PolicySet]:
    """Load policy from environment variable SAFELAYER_POLICY."""
    policy_file = os.getenv('SAFELAYER_POLICY')
    if policy_file and Path(policy_file).exists():
        manager = get_policy_manager()
        policy = manager.load_policy(policy_file)
        manager.set_active_policy(policy.name)
        return policy
    return None
