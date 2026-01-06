"""
AI信息分析系统 - 文件管理模块

本模块负责管理三层文件夹的文件操作，包括：
- 扫描input文件夹获取待处理文件
- 将处理结果保存到processing文件夹
- 管理文件的归档和移动
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .config import INPUT_DIR, PROCESSING_DIR, OUTPUT_DIR, NamingConfig


class FileManager:
    """文件管理器"""
    
    def __init__(self):
        """初始化文件管理器"""
        self.input_dir = INPUT_DIR
        self.processing_dir = PROCESSING_DIR
        self.output_dir = OUTPUT_DIR
        
    def get_pending_files(self, extension: str = ".md") -> List[Path]:
        """
        获取input文件夹中待处理的文件
        
        Args:
            extension: 文件扩展名，默认为.md
            
        Returns:
            待处理文件路径列表
        """
        pending_files = []
        for file_path in self.input_dir.glob(f"*{extension}"):
            # 排除README文件
            if file_path.name.lower() != "readme.md":
                pending_files.append(file_path)
        
        # 按文件名排序（通常包含日期）
        return sorted(pending_files)
    
    def get_files_by_date(
        self, 
        date: str, 
        directory: str = "input"
    ) -> List[Path]:
        """
        获取指定日期的文件
        
        Args:
            date: 日期字符串，格式为YYYY-MM-DD
            directory: 目录类型（input/processing/output）
            
        Returns:
            匹配的文件路径列表
        """
        dir_map = {
            "input": self.input_dir,
            "processing": self.processing_dir,
            "output": self.output_dir,
        }
        target_dir = dir_map.get(directory, self.input_dir)
        
        matching_files = []
        for file_path in target_dir.glob(f"{date}*.md"):
            matching_files.append(file_path)
            
        return sorted(matching_files)
    
    def get_files_in_date_range(
        self,
        start_date: str,
        end_date: str,
        directory: str = "processing"
    ) -> List[Path]:
        """
        获取日期范围内的文件
        
        Args:
            start_date: 开始日期，格式为YYYY-MM-DD
            end_date: 结束日期，格式为YYYY-MM-DD
            directory: 目录类型
            
        Returns:
            匹配的文件路径列表
        """
        dir_map = {
            "input": self.input_dir,
            "processing": self.processing_dir,
            "output": self.output_dir,
        }
        target_dir = dir_map.get(directory, self.processing_dir)
        
        start = datetime.strptime(start_date, NamingConfig.DATE_FORMAT)
        end = datetime.strptime(end_date, NamingConfig.DATE_FORMAT)
        
        matching_files = []
        for file_path in target_dir.glob("*.md"):
            if file_path.name.lower() == "readme.md":
                continue
                
            # 尝试从文件名提取日期
            file_date_str = file_path.stem[:10]  # YYYY-MM-DD
            try:
                file_date = datetime.strptime(
                    file_date_str, 
                    NamingConfig.DATE_FORMAT
                )
                if start <= file_date <= end:
                    matching_files.append(file_path)
            except ValueError:
                # 文件名不符合日期格式，跳过
                continue
                
        return sorted(matching_files)
    
    def save_to_processing(
        self, 
        content: str, 
        filename: str
    ) -> Path:
        """
        保存内容到processing文件夹
        
        Args:
            content: 要保存的内容
            filename: 文件名
            
        Returns:
            保存的文件路径
        """
        file_path = self.processing_dir / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path
    
    def save_to_output(
        self, 
        content: str, 
        filename: str,
        subfolder: Optional[str] = None
    ) -> Path:
        """
        保存内容到output文件夹
        
        Args:
            content: 要保存的内容
            filename: 文件名
            subfolder: 可选的子文件夹（notes/decisions/knowledge）
            
        Returns:
            保存的文件路径
        """
        if subfolder:
            target_dir = self.output_dir / subfolder
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            target_dir = self.output_dir
            
        file_path = target_dir / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path
    
    def move_to_archive(
        self, 
        file_path: Path, 
        archive_name: str = "archive"
    ) -> Path:
        """
        将文件移动到归档目录
        
        Args:
            file_path: 要归档的文件路径
            archive_name: 归档目录名
            
        Returns:
            归档后的文件路径
        """
        archive_dir = file_path.parent / archive_name
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = archive_dir / file_path.name
        shutil.move(str(file_path), str(dest_path))
        return dest_path
    
    def read_file(self, file_path: Path) -> str:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容字符串
        """
        return file_path.read_text(encoding="utf-8")
    
    def list_all_files(self, directory: str = "all") -> dict:
        """
        列出所有文件
        
        Args:
            directory: 目录类型（input/processing/output/all）
            
        Returns:
            文件列表字典
        """
        result = {}
        
        dirs_to_scan = []
        if directory == "all":
            dirs_to_scan = [
                ("input", self.input_dir),
                ("processing", self.processing_dir),
                ("output", self.output_dir),
            ]
        else:
            dir_map = {
                "input": self.input_dir,
                "processing": self.processing_dir,
                "output": self.output_dir,
            }
            if directory in dir_map:
                dirs_to_scan = [(directory, dir_map[directory])]
        
        for dir_name, dir_path in dirs_to_scan:
            files = []
            for file_path in dir_path.rglob("*.md"):
                if file_path.name.lower() != "readme.md":
                    files.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat(),
                    })
            result[dir_name] = sorted(files, key=lambda x: x["name"])
            
        return result


# 模块级别的便捷实例
file_manager = FileManager()
