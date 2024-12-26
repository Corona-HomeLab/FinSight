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
    namespace: str
    data_type: str = "general"
    params: Optional[dict] = {}
    headers: Optional[dict] = {}
    data_key: Optional[str] = None
    active: bool = True
    added_at: datetime = datetime.now()
    document_ids: Optional[list] = []
    
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
                logging.info(f"Loading sources from {self.config_path}")
                with open(self.config_path, 'r') as f:
                    try:
                        data = json.load(f)
                        logging.info(f"Loaded data: {json.dumps(data, indent=2)}")
                        for source_id, source_data in data.items():
                            source_data['added_at'] = datetime.fromisoformat(source_data['added_at'])
                            self.sources[source_id] = APISourceConfig(**source_data)
                        logging.info(f"Loaded {len(self.sources)} sources")
                    except json.JSONDecodeError:
                        logging.error("JSON file is corrupted")
                        self.sources = {}
                        if os.path.exists(self.config_path):
                            backup_path = f"{self.config_path}.bak"
                            os.rename(self.config_path, backup_path)
            else:
                logging.info(f"No config file found at {self.config_path}")
                self.sources = {}
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
        """Remove a source completely"""
        if source_id in self.sources:
            logging.info(f"Removing source {source_id} from sources")
            del self.sources[source_id]  # Actually delete the source
            self._save_sources()
            logging.info(f"Source {source_id} removed and config saved")
        else:
            logging.warning(f"Source {source_id} not found in sources")
    
    def get_active_sources(self) -> Dict[str, APISourceConfig]:
        """Get all active sources"""
        active_sources = {id: source for id, source in self.sources.items() if source.active}
        logging.info(f"Found {len(active_sources)} active sources out of {len(self.sources)} total sources")
        return active_sources
