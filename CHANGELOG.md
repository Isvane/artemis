# Changelog

## [0.2.0](https://github.com/Isvane/artemis/compare/v0.1.0...v0.2.0) (2026-06-17)


### Features

* add CRUD routes for projects and nested jobs ([ac4e241](https://github.com/Isvane/artemis/commit/ac4e241e686dd8962a9f4998cfdd6b545a251ae8))
* add project and job models with alembic migration ([cfd0797](https://github.com/Isvane/artemis/commit/cfd079725e7eca83dccc6c68789698775502925d))
* add pydantic schemas for project and job models ([e9262f1](https://github.com/Isvane/artemis/commit/e9262f195bf1d9b29240252741e055cf250e86fb))
* add pydantic schemas for user ([39955e9](https://github.com/Isvane/artemis/commit/39955e9c0472e282d80b143222ca83a321ce1d46))
* add user model and establish 1-to-many relationship with projects ([465b261](https://github.com/Isvane/artemis/commit/465b261c57e9cbee947e6ff69dc0c80ce8083fcc))
* **api:** restrict project access to authenticated owners ([7a79062](https://github.com/Isvane/artemis/commit/7a7906244e83ff8afe89876846359056a6b632f0))
* **auth:** implement registration and login endpoints with test suite ([810bb81](https://github.com/Isvane/artemis/commit/810bb81fba17da58b9827c4e46290e5ab7d558b2))
* **core:** add core security utility with Argon2 and JWT ([3d949bc](https://github.com/Isvane/artemis/commit/3d949bc758ded423e34f43d98573f56f02fc02ec))
* **deps:** add get_current_user dependency ([7076618](https://github.com/Isvane/artemis/commit/7076618cd95a886275291effa6309d8539359117))
* implement user CRUD operations ([658fc31](https://github.com/Isvane/artemis/commit/658fc31bf176c6ce5bff0d56d5b73c576d9ddf04))
* integrate Prometheus and Grafana for application monitoring ([e3f20ae](https://github.com/Isvane/artemis/commit/e3f20ae56d2d066f1bc1cae1417d8a3c12435e99))


### Documentation

* update README.md ([38c4f52](https://github.com/Isvane/artemis/commit/38c4f52a4fab98d6bb9341a248d922fbf0d3e076))

## 0.1.0 (2026-06-07)


### Features

* implement FastAPI lifespan to manage global HTTPX client ([c35fdae](https://github.com/Isvane/artemis/commit/c35fdae411aec88b1e79ebba965a47b81fb97991))
* setup asynchronous Alembic migration environment ([2a942bb](https://github.com/Isvane/artemis/commit/2a942bb36ab3e75e72bc77282c0f6ceb732dd6df))
* setup containerized environment and async database connection ([a30da32](https://github.com/Isvane/artemis/commit/a30da32bba0870ae74f1978b3094c3a2c1626f6f))


### Bug Fixes

* resolve object is not callable issue in config ([a523d8a](https://github.com/Isvane/artemis/commit/a523d8a21ae8c7fb8ae28f87ce6687aeba6caa23))


### Documentation

* add initial README with project overview and tech stack ([3210d9c](https://github.com/Isvane/artemis/commit/3210d9c4d3cf6a493138b42b260fa15b045fb4a3))
