import os
import shutil
import sys
from pathlib import Path
from transformers import generate_page, generate_pages_recursive


def copy_directory_contents(src: str, dst: str) -> None:
    
    src = os.path.abspath(os.path.expanduser(src))
    dst = os.path.abspath(os.path.expanduser(dst))

    print(f"Copying from {src} to {dst}")

    Path(dst).mkdir(parents=True, exist_ok=True)

    print(f"Cleaning destination {dst}")
    for item in os.listdir(dst):
        item_path = os.path.join(dst, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            print(f"Deleting file: {item_path}")
            os.unlink(item_path)
        else:
            print(f"Deleting directory: {item_path}")
            shutil.rmtree(item_path)
    
    def _copy_recursive(current_src: str, current_dst: str) -> None:
        for item in os.listdir(current_src):
            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isfile(src_path):
                print(f"Copying file: {src_path} -> {dst_path}")
                shutil.copy2(src_path, dst_path)
            elif os.path.isdir(src_path):
                print(f"Creating directory: {dst_path}")
                os.makedirs(dst_path, exist_ok=True)
                _copy_recursive(src_path, dst_path)
    
    
    _copy_recursive(src, dst)
    print("Copy complete!")

def main():
    project_root = Path(__file__).parent.parent
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/" #new

    copy_directory_contents(str(project_root / "static"), str(project_root / "docs")) #changed from public to docs

    generate_pages_recursive(str(project_root / "content"), str(project_root / "template.html"), str(project_root / "docs"), base_path) #changed from public to docs, added base_path



if __name__ == "__main__":
    main()