
# May need to run twice on first pull to copy styles
all:
	python easy_pres.py DCDW_pyparsing.markdown --output index.html

compile:
	git checkout --orphan gh-pages
	git add index.html
	git add css
	git add js
	git commit -a -m "Webpage commit"
	git push origin gh-pages
	git checkout origin

push:
	git add *.markdown
	git status
	-git commit -a
	git push
pull:
	git pull
view:
	chromium-browser index.html
clean:
	rm -rvf css js index.html