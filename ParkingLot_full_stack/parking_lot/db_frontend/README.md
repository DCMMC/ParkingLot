## Getting started

```bash
# install dependency
yarn install

# develop
yarn run dev
```

This will automatically open http://localhost:9527

## Build

```bash
# build for test environment
yarn run build:stage

# build for production environment
yarn run build:prod
```

## Advanced

```bash
# preview the release environment effect
yarn run preview

# preview the release environment effect + static resource analysis
yarn run preview -- --report

# code format check
yarn run lint

# code format check and auto fix
yarn run lint -- --fix
```
