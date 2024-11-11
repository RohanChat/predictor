import json
import io  # Import io for handling file encoding

def extract_outputs(notebook_path, output_path):
    try:
        with io.open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except IOError:
        print("Error: The notebook file does not exist or cannot be read.")
        return
    except ValueError:
        print("Error: The notebook file is not valid JSON.")
        return

    outputs = []
    cell_count = 0
    output_count = 0

    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            cell_count += 1
            for output in cell.get('outputs', []):
                output_count += 1
                if output.get('output_type') == 'stream' and output.get('name') == 'stdout':
                    text = ''.join(output.get('text', []))
                    outputs.append("### Output {0} from Cell {1} ###\n{2}\n".format(output_count, cell_count, text))
                elif output.get('output_type') in ['execute_result', 'display_data']:
                    data = output.get('data', {})
                    text = data.get('text/plain', '')
                    outputs.append("### Output {0} from Cell {1} ###\n{2}\n".format(output_count, cell_count, text))
                elif output.get('output_type') == 'error':
                    ename = output.get('ename', '')
                    evalue = output.get('evalue', '')
                    traceback = '\n'.join(output.get('traceback', []))
                    error_output = "{0}: {1}\n{2}\n".format(ename, evalue, traceback)
                    outputs.append("### Output {0} from Cell {1} ###\n{2}\n".format(output_count, cell_count, error_output))

    if not outputs:
        print("No outputs found in the notebook.")
        return

    try:
        with io.open(output_path, 'w', encoding='utf-8') as f_out:
            for output in outputs:
                f_out.write(output + u"\n")
        print("All outputs have been extracted to '{0}'.".format(output_path))
    except IOError:
        print("Error: Cannot write to the output file.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python extract_outputs_legacy.py <notebook.ipynb> <output.txt>")
        sys.exit(1)
    
    notebook_file = sys.argv[1]
    output_file = sys.argv[2]
    extract_outputs(notebook_file, output_file)
