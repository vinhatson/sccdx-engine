# Deploying to a Hugging Face Space

This puts a **live, hosted** copy of the engine online, so anyone can use it
without installing Python. It is the single biggest thing you can do for
reach: the GitHub repository asks a visitor to clone and install; a Space asks
them to click a link.

The Space runs the same `serve.py` with no code change — it already reads
`SCCDX_HOST` and `SCCDX_PORT` from the environment, and the
[`Dockerfile`](../../Dockerfile) at the repository root sets them to
`0.0.0.0:7860`, which is what Spaces expect.

> **Not yet tested in a live Space.** The Dockerfile was written against the
> Spaces Docker SDK contract (non-root uid 1000, `app_port`) but has not been
> built, because this machine has no Docker. Expect to iterate once on the
> first build, and check the build log if the Space does not come up.

---

## 1. Create the Space

1. Sign in at <https://huggingface.co> (free account).
2. Go to <https://huggingface.co/new-space>.
3. Fill in:
   - **Space name**: `sccdx-engine`
   - **License**: `apache-2.0`
   - **SDK**: **Docker** → **Blank**
   - **Hardware**: `CPU basic` (free) is enough
   - **Visibility**: Public
4. Create it.

## 2. Push the engine into it

A Space is itself a git repository. Clone it, copy the engine in, push.

```bash
git clone https://huggingface.co/spaces/<your-hf-username>/sccdx-engine
cd sccdx-engine

# copy the engine in, but NOT its .git directory
# (adjust the source path to wherever you cloned the GitHub repo)
cp -r /path/to/github/sccdx-engine/{sccd,sccdx,web,sea2027,docs} .
cp /path/to/github/sccdx-engine/{serve.py,api_fastapi.py,validate2.py} .
cp /path/to/github/sccdx-engine/{validate_lang.py,validate_v1.py,requirements.txt} .
cp /path/to/github/sccdx-engine/{Dockerfile,LICENSE,NOTICE} .

# the Space's own README.md must carry the HF frontmatter
cp /path/to/github/sccdx-engine/deploy/huggingface/README.md README.md

git add -A
git commit -m "SCCD-X Engine v2.00"
git push
```

Then watch the build log on the Space page. First build takes a few minutes
because it installs `numpy` and `scipy` and runs `validate2.py` as a build
check.

### A note on size

`sea2027/` is about 12 MB, mostly the 44 PDFs and the two payload JSON files.
That is fine for a Space, but if you would rather keep the Space lean, leave
`sea2027/` out — the engine and the web UI do not need it:

```bash
# minimal Space: skip sea2027/ and docs/
cp -r /path/to/github/sccdx-engine/{sccd,sccdx,web} .
cp /path/to/github/sccdx-engine/{serve.py,validate2.py,validate_lang.py} .
cp /path/to/github/sccdx-engine/{validate_v1.py,Dockerfile,LICENSE,NOTICE} .
```

If you do skip `sea2027/`, drop the `RUN python validate2.py` line from the
Dockerfile — some of the 119 checks read files under `sea2027/`.

## 3. Fill in the link

The Space README has a `REPO_SLUG` placeholder. Replace it with your GitHub
path, for example `vinhatson/sccdx-engine`, so the Space points back at the
source.

## 4. Link the two together

- On the **GitHub** repo: add the Space URL to the repository description and
  the About sidebar.
- On the **Space**: the README already links back to GitHub.

Two-way links matter more than they look. People arrive at one and want the
other, and a Space with no source link reads as a toy.

---

## Troubleshooting the build

**Build succeeds, Space shows "no application file"**
`app_port: 7860` is missing from the README frontmatter, or the container is
listening on a different port. Check that `SCCDX_HOST=0.0.0.0` — binding to
`127.0.0.1` inside a container makes the app unreachable from outside it.

**Build fails at `RUN python validate2.py`**
That line is deliberate: it refuses to ship an image whose engine does not
pass its own checks. Read the output to see which check failed. If you built a
minimal Space without `sea2027/`, remove the line.

**Permission errors**
Spaces run as uid 1000 and the image must not require root. The Dockerfile
creates the `app` user and `chown`s the copied files; if you add files after
the `USER app` line, they will be owned by root and may not be readable.

**It works but it is slow to wake**
Free Spaces sleep when idle and take a few seconds to wake. That is expected.

---

## Why not put `amr-engine` on a Space too?

It does not need one. Its three panels are self-contained HTML and run on
GitHub Pages with no server at all — which is both cheaper and faster than a
Space. See that repository's landing page.

`sccdx-engine` needs a Space precisely because it computes its diagnosis
server-side on purpose, so the page cannot be made static without giving up
the property that every string arrives from the API.
