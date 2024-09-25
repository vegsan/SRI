import os


def generate_nav(parent_dir, nav_name, ignore=[]):
    """
    Recursively traverses a directory tree starting at parent_dir
    and generates a nav.yml file in the same directory, with a list
    of all files and directories in alphabetical order, indented based
    on their depth, and with their full paths (except for the parent_dir)
    """
    def traverse_dir(curr_dir, depth, ignore):
        """
        Recursive function that traverses the directory tree starting
        at curr_dir and generates the YAML list of files and directories
        """
        items = sorted(os.listdir(curr_dir))
        if "index.md" in items:
            index = items.index("index.md")
            items.pop(index)
            items.insert(0, "index.md")
        print(items)
        index_md = None
        for item in items:
            item_path = os.path.join(curr_dir, item)
            if os.path.isdir(item_path):
                if item in ignore:
                    continue
                nav_file.write(f"{'  ' * depth}- {os.path.split(item)[1]}:\n")
                traverse_dir(item_path, depth+1, ignore)
            elif item == "index.md":
                index_md_name = os.path.splitext(os.path.basename(item_path))[0]
                index_md_path = item_path.replace(parent_dir, ".", 1)
                nav_file.write(f"{'  ' * depth}- {index_md_path}\n")
            else:
                item_name = os.path.splitext(item)[0]
                item_path = item_path.replace(parent_dir, ".", 1)
                nav_file.write(f"{'  ' * depth}- {item_name}: {item_path}\n")

    # Create the nav.yml file and write the first line
    with open(nav_name, "w") as nav_file:
        nav_file.write("nav:\n")
        traverse_dir(parent_dir, 1, ignore)


if __name__ == "__main__":
    docs_path = "./docs"
    nav_name = "./nav.yml"
    ignore = ["javascripts","intermezzo","img",".obsidian","melt93"]
    generate_nav(docs_path, nav_name, ignore)

    mkdocs_file_path = "./mkdocs.yml"
    output_file_path = "./mkdocs_new.yml"

    with open(nav_name, "r") as nav_file, \
         open(mkdocs_file_path, "r") as mkdocs_file, \
         open(output_file_path, "w") as output_file:

        for line in mkdocs_file:
            if line.strip() == "nav:":
               break 
            output_file.write(line)
        else:
            print("Error: la sección 'nav:' no se encuentra en el archivo mkdocs.yml")
            exit(1)
        for line in nav_file:
            output_file.write(line)
        output_file.write("\n")
        copia = False
        for line in mkdocs_file:
            if not copia and line.strip() != "":
                continue
            else:
                for line in mkdocs_file:           
                    output_file.write(line)

    os.rename(mkdocs_file_path, mkdocs_file_path + ".bak")
    os.rename(output_file_path, mkdocs_file_path)
