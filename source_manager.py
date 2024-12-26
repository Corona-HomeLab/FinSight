from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl
import json
import os
import logging

class APISourceConfig(BaseModel):
    name: str
    endpoint: HttpUrl
    description: str
    params: Optional[dict] = {}
    headers: Optional[dict] = {}
    data_key: Optional[str] = None
    active: bool = True
    added_at: datetime = datetime.now()
    
    class Config:
        json_encoders = {
            HttpUrl: str
        }

class SourceManager:
    def __init__(self, config_path: str = "sources_config.json"):
        self.config_path = config_path
        self.sources: Dict[str, APISourceConfig] = {}
        self._load_sources()
    
    def _load_sources(self):
        """Load sources from config file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    try:
                        data = json.load(f)
                        for source_id, source_data in data.items():
                            source_data['added_at'] = datetime.fromisoformat(source_data['added_at'])
                            self.sources[source_id] = APISourceConfig(**source_data)
                    except json.JSONDecodeError:
                        # If the file is corrupted, start fresh
                        self.sources = {}
                        # Backup the corrupted file
                        if os.path.exists(self.config_path):
                            backup_path = f"{self.config_path}.bak"
                            os.rename(self.config_path, backup_path)
        except Exception as e:
            logging.error(f"Error loading sources: {str(e)}")
            self.sources = {}
    
    def _save_sources(self):
        """Save sources to config file"""
        try:
            data = {
                source_id: {
                    **source.dict(exclude={'endpoint'}),
                    'endpoint': str(source.endpoint),
                    'added_at': source.added_at.isoformat()
                }
                for source_id, source in self.sources.items()
            }
            # Write to a temporary file first
            temp_path = f"{self.config_path}.tmp"
            with open(temp_path, 'w') as f:
                json.dump(data, f, indent=2)
            # Then rename it to the actual config file
            os.replace(temp_path, self.config_path)
        except Exception as e:
            logging.error(f"Error saving sources: {str(e)}")
            raise
    
    def add_source(self, source_id: str, config: dict) -> APISourceConfig:
        """Add a new API source"""
        source = APISourceConfig(**config)
        self.sources[source_id] = source
        self._save_sources()
        return source
    
    def remove_source(self, source_id: str):
        """Deactivate a source"""
        if source_id in self.sources:
            self.sources[source_id].active = False
            self._save_sources()
    
    def get_active_sources(self) -> Dict[str, APISourceConfig]:
        """Get all active sources"""
        return {id: source for id, source in self.sources.items() if source.active}
