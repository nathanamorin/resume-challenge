
deploy: infra_deploy s3_deploy

infra_deploy:
	$(MAKE) -C subdir

s3_deploy:
	aws s3 cp --recursive site s3://nathan-morin-static-resume-site/
