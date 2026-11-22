# danieltschumi.ch

Personal landing page for [danieltschumi.ch](https://danieltschumi.ch/).

One static page: plain HTML, CSS and JavaScript, no frameworks, no build step, no external requests.
The pixel-art avatar is an inline SVG. Its eyes follow the cursor, it blinks, it ducks behind the laptop on hover and it raises its eyebrows when a link is hovered.

## Structure

```
index.html            the page, including the inline avatar SVG
robots.txt            crawler rules (allow all)
.htaccess             hides repo-only files (tools/, README, LICENSE, dotfiles) on the server
assets/css/site.css   styles (light/dark theme tokens, layout, avatar motion)
assets/js/site.js     theme toggle, Swiss local clock, avatar behaviour
assets/fonts/         self-hosted Inter Tight and JetBrains Mono (latin subset, SIL OFL)
assets/img/           favicons
tools/pixel-avatar.py generator for the avatar artwork (not used by the page)
```

## Local preview

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

## Editing the avatar

The avatar is generated from `tools/pixel-avatar.py`. Change the colours or shapes there, then run:

```sh
python3 tools/pixel-avatar.py
```

This rewrites the avatar block in `index.html` and leaves the rest of the page untouched.

## Deploy

Upload `index.html` and the `assets/` folder to the webspace. Leave out `tools/`, `README.md`, `LICENSE` and the git files.

## License

Code: MIT, see [LICENSE](LICENSE).
Fonts: SIL Open Font License 1.1, see `assets/fonts/OFL-*.txt`.
