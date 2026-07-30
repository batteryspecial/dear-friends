## dear-friends
A Vue.js and Django REST Framework project. Run frontend and backend concurrently from project root (venv required), or run them separately.

```
% npm run dev
> dev
> npm --prefix frontend run dev


> frontend@0.0.0 dev
> concurrently -n frontend,backend -c blue,green "vite" "cd ../backend && ../.venv/bin/python manage.py runserver --noreload --nothreading --skip-checks"
```

You can also start up the client and server separately.

```
% cd frontend && npm run dev
...
% source .venv/bin/activate
(.venv) % cd backend && python manage.py runserver
...
```

Feel free to configure your own TTS or alternative ASR options (project currently uses mlx-whisper and faster-whisper, which runs on CPU).
