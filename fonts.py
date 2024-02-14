import os
import requests
from tqdm import tqdm

# Define where font will be stored
fonts_dir_relative = os.path.join('static', 'fonts')
fonts_dir_absolute = os.path.join(os.path.split(os.path.realpath(__file__))[0], fonts_dir_relative)

# Define which font family to use (e.g. 'noto-sans' or 'noto-serif')
# font_family = "noto-sans"
font_family = "noto-serif"

# Define all fonts
fonts = {
    'families': [
        {'name': 'noto-sans', 'fonts':
            [  # Noto Sans. Use CJK SC for English
                {'name': 'Noto Sans', 'lang': 'en', 'fallback': 'sans-serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/OTF/NotoSansCJKsc-VF.otf'},
                {'name': 'Noto Sans SC', 'lang': 'sc', 'fallback': 'sans-serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/OTF/NotoSansCJKsc-VF.otf'},
                {'name': 'Noto Sans TC', 'lang': 'tc', 'fallback': 'sans-serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/OTF/NotoSansCJKtc-VF.otf'},
                {'name': 'Noto Sans JP', 'lang': 'ja', 'fallback': 'sans-serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/OTF/NotoSansCJKjp-VF.otf'},
                {'name': 'Noto Sans KR', 'lang': 'ko', 'fallback': 'sans-serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/OTF/NotoSansCJKkr-VF.otf'},
            ]
         },
        {'name': 'noto-serif', 'fonts':
            [  # Noto Serif. Use CJK SC for English
                {'name': 'Noto Serif', 'lang': 'en', 'fallback': 'serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Serif/Variable/OTF/NotoSerifCJKsc-VF.otf'},
                {'name': 'Noto Serif SC', 'lang': 'sc', 'fallback': 'serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Serif/Variable/OTF/NotoSerifCJKsc-VF.otf'},
                {'name': 'Noto Serif TC', 'lang': 'tc', 'fallback': 'serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Serif/Variable/OTF/NotoSerifCJKtc-VF.otf'},
                {'name': 'Noto Serif JP', 'lang': 'ja', 'fallback': 'serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Serif/Variable/OTF/NotoSerifCJKjp-VF.otf'},
                {'name': 'Noto Serif KR', 'lang': 'ko', 'fallback': 'serif',
                 'url': 'https://github.com/notofonts/noto-cjk/raw/main/Serif/Variable/OTF/NotoSerifCJKkr-VF.otf'}
            ]
         }
    ]
}


def _download_file(url, output_path):
    temp_path = output_path + '.tmp'  # Temporary file path
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()  # Check for errors
        total_size = int(r.headers.get('content-length', 0))
        with open(temp_path, 'wb') as f, tqdm(
                total=total_size, unit='B', unit_scale=True, desc=output_path,
                ascii=True, leave=False) as pbar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))

    # Rename the temporary file to the target file after download is completed
    os.rename(temp_path, output_path)


def download_fonts():
    for family in fonts['families']:
        for font in family['fonts']:
            filename = os.path.split(font['url'])[-1]
            filepath_absolute = os.path.join(fonts_dir_absolute, filename)
            filepath_relative = os.path.join(fonts_dir_relative, filename)

            if os.name == 'nt':
                filepath_relative = filepath_relative.replace('\\', '/')

            font.update({'path': filepath_relative})  # Update relative path in the font dict

            if not os.path.exists(filepath_absolute):  # Download if file not exiets
                print('Downloading font: {}'.format(font['url']))
                _download_file(font['url'], filepath_absolute)


if __name__ == '__main__':
    download_fonts()
