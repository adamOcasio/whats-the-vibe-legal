# what's the vibe? legal pages

Public pages for the what's the vibe? NYC app, served by GitHub Pages:

- Privacy policy: https://adamocasio.github.io/whats-the-vibe-legal/privacy/

The policy's source is `PRIVACY_POLICY.md` in the app's (private) repository; change both together.

Rebuild the page after changing the policy:

```sh
python3 build_policy.py <app repository>/PRIVACY_POLICY.md privacy/index.html
```
