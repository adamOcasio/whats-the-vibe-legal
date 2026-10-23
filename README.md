# what's the vibe? legal pages

Public pages for the what's the vibe? NYC app, served by GitHub Pages:

- Privacy policy: https://adamocasio.github.io/whats-the-vibe-legal/privacy/
- Terms of use: https://adamocasio.github.io/whats-the-vibe-legal/terms/
- Support (the home page, the App Store's Support URL): https://adamocasio.github.io/whats-the-vibe-legal/
- Get the app: https://adamocasio.github.io/whats-the-vibe-legal/get/ forwards to the public TestFlight link
  (`https://testflight.apple.com/join/Da4VhdAN`). Printed QR codes point here, so keep this URL and change only
  where `get/index.html` sends people (its three links), for example to the App Store listing at launch.

Their sources are `PRIVACY_POLICY.md` and `TERMS_OF_USE.md` in the app's (private) repository; change
each page together with its source.

Rebuild a page after changing its source:

```sh
python3 build_policy.py <app repository>/PRIVACY_POLICY.md privacy/index.html
python3 build_policy.py <app repository>/TERMS_OF_USE.md terms/index.html "Terms of use" "The rules for using the what’s the vibe? app, with no tolerance for objectionable content or abusive users."
```
