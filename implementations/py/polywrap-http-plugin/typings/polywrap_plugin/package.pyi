"""
This type stub file was generated by pyright.
"""

from typing import Generic, Optional, TypeVar
from polywrap_core import GetManifestOptions, IWrapPackage, Wrapper
from polywrap_manifest import AnyWrapManifest
from polywrap_result import Result
from .module import PluginModule

TConfig = TypeVar("TConfig")
class PluginPackage(Generic[TConfig], IWrapPackage):
    module: PluginModule[TConfig]
    manifest: AnyWrapManifest
    def __init__(self, module: PluginModule[TConfig], manifest: AnyWrapManifest) -> None:
        ...
    
    async def create_wrapper(self) -> Result[Wrapper]:
        ...
    
    async def get_manifest(self, options: Optional[GetManifestOptions] = ...) -> Result[AnyWrapManifest]:
        ...
    


