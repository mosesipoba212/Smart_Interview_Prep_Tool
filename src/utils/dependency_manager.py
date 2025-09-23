"""
Enhanced Dependency Manager
Handles missing modules gracefully with fallback implementations
"""

import importlib
import sys
from typing import Dict, Any, Optional, Callable

class DependencyManager:
    """Manages optional dependencies and provides fallbacks"""
    
    def __init__(self):
        self.available_modules = {}
        self.fallback_implementations = {}
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check availability of all dependencies"""
        dependencies = {
            # Core dependencies (required)
            'flask': {'required': True, 'import_name': 'flask'},
            'requests': {'required': True, 'import_name': 'requests'},
            'dotenv': {'required': True, 'import_name': 'dotenv'},
            
            # Optional dependencies
            'openai': {'required': False, 'import_name': 'openai'},
            'docx': {'required': False, 'import_name': 'docx'},
            'matplotlib': {'required': False, 'import_name': 'matplotlib'},
            'pandas': {'required': False, 'import_name': 'pandas'},
            'seaborn': {'required': False, 'import_name': 'seaborn'},
            'sqlite3': {'required': False, 'import_name': 'sqlite3'},
        }
        
        for module_name, config in dependencies.items():
            try:
                module = importlib.import_module(config['import_name'])
                self.available_modules[module_name] = module
                print(f"✅ {module_name} available")
            except ImportError as e:
                self.available_modules[module_name] = None
                if config['required']:
                    print(f"❌ Required module {module_name} missing: {e}")
                    raise ImportError(f"Required dependency {module_name} not found")
                else:
                    print(f"⚠️ Optional module {module_name} not available - using fallback")
    
    def get_module(self, module_name: str, fallback: Optional[Callable] = None):
        """Get module or return fallback"""
        module = self.available_modules.get(module_name)
        if module is not None:
            return module
        
        if fallback:
            return fallback()
        
        # Return a mock module for graceful degradation
        return self.create_mock_module(module_name)
    
    def create_mock_module(self, module_name: str):
        """Create a mock module that logs usage attempts"""
        class MockModule:
            def __getattr__(self, name):
                print(f"⚠️ Attempted to use {module_name}.{name} but {module_name} is not available")
                return lambda *args, **kwargs: None
        
        return MockModule()
    
    def is_available(self, module_name: str) -> bool:
        """Check if a module is available"""
        return self.available_modules.get(module_name) is not None
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive dependency status report"""
        return {
            'available': {name: module is not None 
                         for name, module in self.available_modules.items()},
            'missing': [name for name, module in self.available_modules.items() 
                       if module is None],
            'total_modules': len(self.available_modules),
            'available_count': sum(1 for module in self.available_modules.values() 
                                 if module is not None)
        }

# Global dependency manager instance
dependency_manager = DependencyManager()

def safe_import(module_name: str, fallback: Optional[Callable] = None):
    """Safely import a module with fallback"""
    return dependency_manager.get_module(module_name, fallback)

def check_module_availability(module_name: str) -> bool:
    """Check if a module is available"""
    return dependency_manager.is_available(module_name)

def get_dependency_status() -> Dict[str, Any]:
    """Get dependency status report"""
    return dependency_manager.get_status_report()

if __name__ == "__main__":
    # Test dependency management
    print("🔧 Testing Enhanced Dependency Management")
    
    status = get_dependency_status()
    print(f"📊 Available modules: {status['available_count']}/{status['total_modules']}")
    
    if status['missing']:
        print(f"⚠️ Missing modules: {', '.join(status['missing'])}")
    
    print("✨ Dependency management system ready!")