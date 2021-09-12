bump:
	pip show jaynes | grep Version | sed 's/Version:\ //g' > VERSION
	git add VERSION
	git ci -m "bump version"
release:
	git tag v$(VERSION) -m '$(msg)'
	git push origin --tags
