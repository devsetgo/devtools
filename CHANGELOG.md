# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Todo
- Document Process (blog entry)
- Increase test coverage
- Add tests for authentication

## [Unreleased]
- nothing


## [20.03.07] - GitHub Oauth Docker
### Added
- Update of Dockerfile and Docker-Compose for passing ENV variables
- Update of login button for Github icon

## [20.01.12] - GitHub Oauth
### Added
- Base of [encode/hostedapi](https://github.com/encode/hostedapi)
    - Use OAuth from Github
    - Mock GitHub OAuth for testing
    - Working on Tests for OAuth
- Profile Page
 - Data from your Github public data

## [19.10.06] - 2019-10-06
### Added
- Tests and file functions
- SonarCloud scan
- Flake8 Cleanup (lot more to do)
- GitHub Actions
    - docker build
    - tests
### Changed
- Change of template to Sufee Admin (previous templates has lots of code issues or were very out of date)

## [19.8.21] - 2019-08-09
### Added
- Tests for file functions
- Tests for main class
### Changed
- exception handling for call_api() function.

## [19.8.9] - 2019-08-09
### Added
- Example templates from SRTDashboard
- Home and example route
- Docker image build and docker-compose
- database setup (not used yet)
- API call to [Test-API](https://github.com/devsetgo/test-api)
- Gunicorn configuration
- Logging via [Loguru](https://github.com/Delgan/loguru)
- Basic document with screenshots

### Changed
- Nothing

### Removed
- Nothing
