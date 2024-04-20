import sys
import json

def validate_title(title: str) -> str:
    """
    Validate title from JSON data

    Params:
        - title (str): title fetched from JSON data

    Return:
        - title (str): validated title
    """
    if not isinstance(title, str):
        raise ValueError("Title should be a string. Please check your code.")
    
    return title

def validate_color(color: str) -> str:
    """
    Validate color from JSON data
    
    Params:
        - color (str): color fetched from JSON data

    Return:
        - color (str): validated color
    """
    if not isinstance(color, str):
        raise ValueError("Color should be a string. Please check your code.")
    
    if not color.startswith('#'):
        raise ValueError("Color should start with #. Please check your code.")
    
    return color

def validate_size(sizes: list) -> list:
    """
    Validate sizes from JSON data

    Params:
        - sizes (list): sizes fetched from JSON data

    Return:
        - sizes (list): validated sizes
    """
    try:
        width = int(sizes[0])
        height = int(sizes[1])
    except (TypeError, IndexError):
        raise ValueError("Cannot parse size to integer. Please check your settings.")
    
    return [width, height]

def validate_frame(frames: list) -> list:
    """
    Validate frames from JSON data

    Params:
        - frames (list): frames fetched from JSON data

    Return:
        - frames (list): validated frames
    """
    if not isinstance(frames, list):
        raise ValueError("Frames should be a list of list. Please check your code.")
    
    for frame in frames:
        if not isinstance(frame, list):
            raise ValueError("Frames should be a list of list. Please check your code.")
        for object in frame:
            if not isinstance(object, str):
                raise ValueError("Frame's content should be a string. Please check your code.")
    
    return frames

def validate_config(config: str) -> str:
    """
    Validate sizes from JSON data

    Params:
        - sizes (list): sizes fetched from JSON data

    Return:
        - sizes (list): validated sizes
    """
    try:
        config_json = json.loads(config)
    except ValueError:
        raise ValueError("Cannot parse Reveal's config to JSON. Please check your settings.") 
    
    return json.dumps(config_json)

def json_to_html(json_data: dict) -> str:
    """
    Convert JSON data to HTML
    
    Params:
        - json_data (dict): a JSON data fetched from codeslide.net
    
    Return:
        - html_output (str): an HTML output
    """
    title = validate_title(json_data['title'])
    color = validate_color(json_data['backgroundColor'])
    sizes = validate_size(json_data['size'])
    frames = validate_frame(json_data['frame'])
    config = validate_config(json_data['config'])
        
    html_output = f"<!doctype html>\n \
    <html lang=\"en\">\n \
	<head>\n \
		<meta charset=\"utf-8\">\n \
		<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">\n \
		<title>{title} - Presentation</title>\n \
        <!-- Favicon -->\n \
        <link rel='apple-touch-icon' sizes='180x180' href='dist/favicon/apple-touch-icon.png'>\n \
        <link rel='icon' type='image/png' sizes='32x32' href='dist/favicon/favicon-32x32.png'>\n \
        <link rel='icon' type='image/png' sizes='16x16' href='dist/favicon/favicon-16x16.png'>\n \
        <link rel='manifest' href='dist/favicon/site.webmanifest'>\n \
        <!-- Reveal.js theme -->\n \
		<link rel=\"stylesheet\" href=\"dist/reset.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/reveal.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/theme/black.css\">\n \
		<link rel=\"stylesheet\" href=\"plugin/highlight/monokai.css\">\n \
	</head>\n \
	<body>\n \
		<div class=\"reveal\">\n \
			<div class=\"slides\">\n \
                <section data-transition=\"fade\">\n \
                    <div class=\"editor\" style=\"background: {color}\">\n \
					    <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {sizes[0]} {sizes[1]}\">\n "
    
    for i in range(len(frames)):
        for svg in frames[i]:
            if i == 0:
                html_output += f'<g class=\"fragment fade-out\" data-fragment-index=\"{i+1}\"> {svg} </g>\n ' 
            elif i == len(frames) - 1:
                html_output += f'<g class=\"fragment\" data-fragment-index=\"{i}\"> {svg} </g>\n ' 
            else:
                html_output += f'<g class=\"fragment fade-in-then-out\" data-fragment-index=\"{i}\"> {svg} </g>\n '
    			
    html_output += f"</svg>\n \
                    </div>\n \
                </section>\n \
            </div>\n \
		</div>\n \
		<script src=\"dist/reveal.js\"></script>\n \
		<script> Reveal.initialize({config}); </script>\n \
	</body>\n \
    </html>"
			
    return html_output

def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    with open(input_file_path, 'r') as file:
        data = json.load(file)
    with open(output_file_path, 'w') as file:
        file.write(json_to_html(data))

if __name__ == "__main__":
    main()