# GitHub Actions test APK

The `Android test APK` workflow builds a separate, debuggable package (`com.aure.totk.codextest`) from source on an Ubuntu runner using NDK r27.3. It does not package game data, a Turnip driver, or `Lossless.dll`. The LSFG picker remains in the app; select the DLL on the Odin 3 after installing the APK.

## One-time signing key setup

Android needs the same signing certificate on each update. Create a PEM file containing a private key and its certificate on your PC, then save its full contents as the **repository Actions secret** `TOTK_SIGNING_KEY_PEM` in your fork (Settings → Secrets and variables → Actions → New repository secret). Keep the file private and out of Git. For example, in Git Bash with OpenSSL:

```sh
openssl req -x509 -newkey rsa:3072 -nodes -keyout totk-test-key.pem \
  -out totk-test-cert.pem -days 10950 -subj '/CN=TotK Odin 3 test'
cat totk-test-key.pem totk-test-cert.pem > totk-signing-key.pem
```

Paste `totk-signing-key.pem` into the secret, then delete the temporary key files after confirming the secret is saved. Never put the key or `Lossless.dll` in the repository. The same secret signs later builds so Android can update the test app without removing its private data.

## Run and download

Push a commit to your fork or use Actions → Android test APK → Run workflow. When the run completes, open it and download the `totk-r27-lsfg-odin3` artifact. Install the APK on the Odin 3; it installs beside the original app. Because Android keeps each app's files separate, the test package needs its own game setup. In Graphics → Performance → Frame generation, select the DLL you own to enable LSFG.
