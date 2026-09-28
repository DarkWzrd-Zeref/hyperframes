# hyperframes

Local, credit-free [HyperFrames](https://github.com/heygen-com/hyperframes) render. This repository is `DarkWzrd-Zeref/hyperframes`.

`./render.sh` is the only way to run the CLI. It pins `hyperframes@0.8.52` and spawns `doctor`, `check`, or `render` on this machine (headless Chrome and FFmpeg). A guard rejects every other subcommand, including `cloud`, `publish`, and `lambda`, before a process starts. There is no cloud render, no HeyGen hosted render, and no credit path.

## Install

- Node.js 22 or newer
- FFmpeg (`ffmpeg` and `ffprobe` on your PATH)
- Python 3

Check the toolchain:

```bash
./render.sh doctor
```

The first `doctor` or `render` downloads the pinned CLI through `npx`. No HeyGen account.

## Render

```bash
./render.sh check path/to/composition
./render.sh render path/to/composition --output out/clip.mp4 --fps 30
./render.sh poster out/clip.mp4 --output out/clip.jpg --at 2
```

`render` always passes `--quality standard --workers 1 --low-memory-mode`. Flags are not forwarded.

## Rails

- Local render only. `./render.sh cloud`, `./render.sh publish`, and any `--cloud` or `--lambda` flag exit 2 and do not call `npx`.
- The pin lives in `package.json` (`hyperframesPin`) and `hf/__init__.py`. They must match.
- Do not commit rendered MP4s.

## License

Apache 2.0 (`LICENSE`), the same license as the HyperFrames CLI this wrapper pins.
