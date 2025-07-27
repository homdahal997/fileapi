#!/usr/bin/env python
"""
Command line interface for file conversion API
"""
import requests
import os
import argparse
import time
import json

class FileConverterCLI:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        
    def get_formats(self):
        """Get available file formats"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/conversions/formats/")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting formats: {e}")
            return None
    
    def convert_file(self, input_file_path, output_format, output_path=None):
        """Convert a file"""
        if not os.path.exists(input_file_path):
            print(f"Error: File {input_file_path} not found")
            return None
            
        try:
            # Upload and convert
            with open(input_file_path, 'rb') as f:
                files = {'input_file': f}
                data = {'output_format': output_format}
                
                response = requests.post(
                    f"{self.base_url}/api/v1/conversions/convert/",
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()
                
            job_id = result['job_id']
            print(f"Conversion started. Job ID: {job_id}")
            
            # Wait for completion
            while True:
                status_response = requests.get(
                    f"{self.base_url}/api/v1/conversions/jobs/{job_id}/"
                )
                status_response.raise_for_status()
                status_data = status_response.json()
                
                if status_data['status'] == 'completed':
                    print("Conversion completed!")
                    
                    # Download result
                    download_response = requests.get(
                        f"{self.base_url}/api/v1/conversions/jobs/{job_id}/download/"
                    )
                    download_response.raise_for_status()
                    
                    # Save file
                    if not output_path:
                        filename = os.path.basename(input_file_path)
                        name, _ = os.path.splitext(filename)
                        output_path = f"{name}_converted.{output_format}"
                    
                    with open(output_path, 'wb') as f:
                        f.write(download_response.content)
                    
                    print(f"File saved to: {output_path}")
                    return output_path
                    
                elif status_data['status'] == 'failed':
                    print(f"Conversion failed: {status_data.get('error_message', 'Unknown error')}")
                    return None
                    
                else:
                    print(f"Status: {status_data['status']}...")
                    time.sleep(2)
                    
        except requests.RequestException as e:
            print(f"Error during conversion: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='File Converter CLI')
    parser.add_argument('command', choices=['formats', 'convert'], help='Command to execute')
    parser.add_argument('--input', '-i', help='Input file path')
    parser.add_argument('--output-format', '-f', help='Output format')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--url', default='http://127.0.0.1:8000', help='API base URL')
    
    args = parser.parse_args()
    
    cli = FileConverterCLI(args.url)
    
    if args.command == 'formats':
        formats = cli.get_formats()
        if formats:
            print("\nAvailable formats:")
            for format_info in formats['results']:
                if format_info['is_output_supported']:
                    print(f"  {format_info['name']} - {format_info['category']}")
    
    elif args.command == 'convert':
        if not args.input or not args.output_format:
            print("Error: --input and --output-format are required for conversion")
            return
        
        result = cli.convert_file(args.input, args.output_format, args.output)
        if result:
            print(f"Conversion successful: {result}")
        else:
            print("Conversion failed")

if __name__ == '__main__':
    main()
