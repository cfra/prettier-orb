# Prettier Orb

[![CircleCI Build](https://circleci.com/gh/cfra/prettier-orb.svg?style=shield)](https://circleci.com/gh/cfra/prettier-orb "CircleCI Build")
[![Orb Version](https://img.shields.io/endpoint.svg?url=https://badges.circleci.io/orb/cfra/prettier)](https://circleci.com/orbs/registry/orb/cfra/prettier "Orb Version")
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://renovateapp.com/ "Renovate enabled")

CircleCI [orb](https://circleci.com/orbs/) to easily run [Prettier](https://prettier.io/) as part of your CI process.

## Releasing a New Orb Version

1.  Create a Git tag with the version you want to release:
    ```console
    git tag --annotate --message=<version> <version>
    ```
1.  Push the tag:
    ```console
    git push --tags
    ```

The orb will be built and tested on CircleCI. If it passes all tests, it will be submitted to the CircleCI orb registry.

## License

Distributed under the MIT license.

Copyright 2019 reelport GmbH

