# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add the data files
added_files = [
    ('prompt_template/jailbreak_prompts_2023_05_07.csv', 'prompt_template'),
    ('prompt_template/jailbreak_prompts_2023_12_25.csv', 'prompt_template'),
    ('prompt_template/regular_prompts_2023_05_07.csv', 'prompt_template'),
    ('prompt_template/regular_prompts_2023_12_25.csv', 'prompt_template'),
    ('config.yaml', '/'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='IceBreakerApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False if you want a GUI application without console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)