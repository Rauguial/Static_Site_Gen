import os
import shutil
from pathlib import Path



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

if __name__ == "__main__":
    base_dir = os.path.expanduser("~/workspace/github.com/Rauguial/Static_Site_Gen")
    copy_directory_contents(
        os.path.join(base_dir, "static"),
        os.path.join(base_dir, "public")
    )