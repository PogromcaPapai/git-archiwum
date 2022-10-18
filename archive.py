import os
from pathlib import Path
from loguru import logger
from pyzipper import AESZipFile, ZIP_LZMA, WZ_AES
from commons import CONFIG as ALL_CONFIGS

CONFIG = ALL_CONFIGS["archive"]

def archive_files(name: str, files: list[Path]):
    logger.info("Starting the writing process")
    with AESZipFile(name, 'w',
                    compression=ZIP_LZMA,
                    encryption=WZ_AES) as archive:
        archive.setpassword(CONFIG['key'].encode())
        for file in files:
            logger.debug("Writing {}", file.name)
            archive.write(file)
            
if __name__=="__main__":
    archive_files('test.zip', list(Path('test').iterdir()))