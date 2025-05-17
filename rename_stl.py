import os

def rename_stl_first_line(directory):
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(directory):
        # Get all STL files in current directory
        stl_files = [f for f in files if f.endswith('.stl')]
        
        for stl_file in stl_files:
            file_path = os.path.join(root, stl_file)
            new_name = os.path.splitext(stl_file)[0]  # Get filename without extension
            
            try:
                # Read the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                
                # Replace the first line
                if lines:
                    lines[0] = f'solid {new_name}\n'
                
                # Replace the last line if it contains 'endsolid'
                if lines and 'endsolid' in lines[-1]:
                    lines[-1] = f'endsolid {new_name}\n'
                
                # Write back to the file
                with open(file_path, 'w') as file:
                    file.writelines(lines)
                
                print(f'Processed: {file_path}')
            except Exception as e:
                print(f'Error processing {file_path}: {str(e)}')

if __name__ == '__main__':
    stl_directory = 'geometry'  # Directory containing STL files
    rename_stl_first_line(stl_directory) 