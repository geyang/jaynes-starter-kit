VERSION=`< VERSION`

bump:
	pip show jaynes | grep Version | sed 's/Version:\ //g' > VERSION
	git add VERSION
	git ci -m "bump version"
release:
	git tag v$(VERSION)
	git push origin --tags
