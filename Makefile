VERSION=`< VERSION`

default: bump release
	git push
bump:
	pip show jaynes | grep Version | sed 's/Version:\ //g' > VERSION
	git add VERSION
	git ci -m "bump version"
release:
	git tag v$(VERSION)
	git push origin --tags
revert:
	git tag -d v$(VERSION)
	git push origin :refs/tags/v$(VERSION)
