# DontManage UI Starter

This template should help get you started developing custom frontend for DontManage
apps with Vue 3 and the DontManage UI package.

This boilerplate sets up Vue 3, Vue Router, TailwindCSS, and DontManage UI out of
the box.

## Usage

This template is meant to be cloned inside an existing DontManage App. Assuming your
apps name is `todo`. Clone this template in the root folder of your app using `degit`.

```
cd apps/todo
npx degit netchampfaris/frappe-ui-starter frontend
cd frontend
yarn
yarn dev
```

The Vite dev server will start on the port `8080`. This can be changed from `vite.config.js`.
The development server is configured to proxy your dontmanage app (usually running on port `8000`). If you have a site named `todo.test`, open `http://todo.test:8080` in your browser. If you see a button named "Click to send 'ping' request", congratulations!

If you notice the browser URL is `/frontend`, this is the base URL where your frontend app will run in production.
To change this, open `src/router.js` and change the base URL passed to `createWebHistory`.

## Resources

-   [Vue 3](https://v3.vuejs.org/guide/introduction.html)
-   [Vue Router](https://next.router.vuejs.org/guide/)
-   [DontManage UI](https://github.com/dontmanage/frappe-ui)
-   [TailwindCSS](https://tailwindcss.com/docs/utility-first)
-   [Vite](https://vitejs.dev/guide/)
