import os
import sys
import subprocess
import shutil
import logging
from typing import List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('build_log.txt')
    ]
)

class BuildConfig:
    """Configuration settings for the build process"""
    REQUIRED_PACKAGES = [
        'pyinstaller',
        'pyttsx3',
        'SpeechRecognition',
        'requests',
        'Pillow',
        'pyaudio'
    ]
    
    HIDDEN_IMPORTS = [
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'queue'
    ]
    
    BUILD_FILES = ['build', 'Jarvis.spec']
    
    def __init__(self, app_name: str = "Jarvis"):
        self.app_name = app_name
        self.icon_path = Path('assets/jarvis_icon.ico')
        self.settings_file = Path('config/jarvis_settings.json')
        self.main_script = Path('jarvis.py')

class JarvisBuilder:
    """Handles the build process for the Jarvis application"""
    
    def __init__(self, config: BuildConfig):
        self.config = config
        self._validate_paths()

    def _validate_paths(self) -> None:
        """Validate required files exist"""
        if not self.config.main_script.exists():
            raise FileNotFoundError(f"Main script {self.config.main_script} not found")
        
        # Create necessary directories
        self.config.icon_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.settings_file.parent.mkdir(parents=True, exist_ok=True)

    def install_requirements(self) -> None:
        """Install required packages using pip"""
        logging.info("Installing required packages...")
        
        for package in self.config.REQUIRED_PACKAGES:
            try:
                logging.info(f"Installing {package}...")
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    logging.error(f"Failed to install {package}: {result.stderr}")
                    raise RuntimeError(f"Package installation failed: {package}")
            except Exception as e:
                logging.error(f"Error installing {package}: {str(e)}")
                raise

    def _get_pyinstaller_command(self) -> List[str]:
        """Generate PyInstaller command with appropriate options"""
        command = [
            'pyinstaller',
            '--noconfirm',
            '--onedir',
            '--windowed',
            f'--name={self.config.app_name}'
        ]
        
        # Add icon if exists
        if self.config.icon_path.exists():
            command.append(f'--icon={self.config.icon_path}')
        else:
            logging.warning("No icon file found. Using default Windows icon.")
        
        # Add settings file if exists
        if self.config.settings_file.exists():
            command.append(f'--add-data={self.config.settings_file};config')
        
        # Add hidden imports
        for import_name in self.config.HIDDEN_IMPORTS:
            command.append(f'--hidden-import={import_name}')
        
        command.append(str(self.config.main_script))
        return command

    def create_executable(self) -> None:
        """Create the executable using PyInstaller"""
        logging.info("Creating executable...")
        
        try:
            command = self._get_pyinstaller_command()
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode != 0:
                logging.error(f"PyInstaller failed: {result.stderr}")
                raise RuntimeError("Executable creation failed")
            
            logging.info("Executable created successfully")
        except Exception as e:
            logging.error(f"Error creating executable: {str(e)}")
            raise

    def cleanup(self) -> None:
        """Clean up temporary build files"""
        logging.info("Cleaning up build files...")
        
        for file_path in self.config.BUILD_FILES:
            path = Path(file_path)
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                elif path.exists():
                    path.unlink()
            except Exception as e:
                logging.warning(f"Error cleaning up {file_path}: {str(e)}")

def main():
    try:
        # Initialize builder with config
        config = BuildConfig()
        builder = JarvisBuilder(config)
        
        # Execute build process
        builder.install_requirements()
        builder.create_executable()
        builder.cleanup()
        
        logging.info("\nBuild completed successfully!")
        logging.info(f"Your executable can be found in the 'dist/{config.app_name}' folder")
        
        # Additional instructions
        if config.settings_file.exists():
            logging.info(f"\nNote: The settings file will be automatically included in the 'config' folder")
        
    except Exception as e:
        logging.error(f"Build failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()