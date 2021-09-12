release:
	pip show jaynes | grep Version | sed 's/Version:\ //g' > VERSION
	git add .
	git ci -m "bump version"
	git push
	git tag v$(VERSION) -m '$(msg)'
	git push origin --tags
