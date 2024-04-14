import sys
import json

def json_to_html(json_data):
    # Compile to html
    title = json_data['title']
    color = json_data['backgroundColor']
    sizes = json_data['size']
    frames = json_data['frame']
    config = json_data['config']
        
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
			<div class=\"slides\"> \
                <section data-transition=\"fade\"> \
                    <div class=\"editor\" style=\"background: {color}\"> \
					    <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {sizes[0]} {sizes[1]}\">"
    
    for i in range(len(frames)):
        for svg in frames[i]:
            html_output += f'<g class=\"fragment fade-in-then-out\" data-fragment-index=\"{i+1}\"> {svg} </g>' 
    			
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