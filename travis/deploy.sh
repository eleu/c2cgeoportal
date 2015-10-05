#!/bin/bash -e

DO_TAG=false
DEPLOY=false
DOC=false
FINAL=false
BUILD_TAG=false # for rc

if [[ ${TRAVIS_BRANCH} =~ ^(master|[0-9].[0-9])$ ]] && [ ${TRAVIS_PULL_REQUEST} == false ]
then
    DO_TAG=true
    DOC=true
fi

if [[ ${TRAVIS_TAG} =~ ^[0-9].[0-9]+.[0-9]$ ]]
then
    if [ ${TRAVIS_TAG} != $(python setup.py -V) ]
    then
        echo "The tag name doesn't match with the egg version."
        exit 1
    fi
    DEPLOY=true
    FINAL=true
fi

if [[ ${TRAVIS_TAG} =~ ^[0-9].[0-9]+.0rc[0-9]$ ]]
then
    VERSION=`echo ${TRAVIS_TAG} | awk -Frc '{print $1}'`
    if [ ${VERSION} != $(python setup.py -V) ]
    then
        echo "The tag name doesn't match with the egg version."
        exit 1
    fi
    DEPLOY=true
    BUILD_TAG=rc`echo ${TRAVIS_TAG} | awk -Frc '{print $2}'`
fi
if [[ ${TRAVIS_TAG} =~ ^0.0.[0-9a-f]*$ ]]
then
    DEPLOY=true
fi

if [ ${DEPLOY} == true  ] && [ ${TRAVIS_PYTHON_VERSION} == "2.7" ]
then
    echo == Do the release ==

    set -x

    if [ ${BUILD_TAG} != false ]
    then
        .build/venv/bin/python setup.py egg_info --no-date --tag-build "${BUILD_TAG}" bdist_wheel
    else
    if [ ${FINAL} == true ]
        then
            .build/venv/bin/python setup.py egg_info --no-date --tag-build "" bdist_wheel
        else
            .build/venv/bin/python setup.py bdist_wheel
        fi
    fi
fi

if [ ${DOC} == true ]
then
    echo == Build the doc ==

    git checkout c2cgeoportal/locale/*/LC_MESSAGES/*.po
    git fetch origin gh-pages:gh-pages
    git checkout gh-pages

    mkdir ${TRAVIS_BRANCH}
    mv doc/_build/html/* ${TRAVIS_BRANCH}
    git add ${TRAVIS_BRANCH}
    git commit -m "Update documentation for the revision ${TRAVIS_COMMIT}"
    git push origin gh-pages
fi

if [ ${DO_TAG} == true  ] && [ ${TRAVIS_PYTHON_VERSION} == "2.7" ]
then
    echo == Add tag ==

    TAG_NAME=0.0.`git show-ref --head --hash -`
    git tag ${TAG_NAME}
    git push origin ${TAG_NAME}
fi
