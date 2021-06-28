
deploy: infra_deploy s3_deploy invalidate_cache

infra_deploy:
	$(MAKE) -C infra

invalidate_cache:
	$(MAKE) -C infra invalidate_cache

s3_deploy:
	aws s3 cp --recursive site s3://nathan-morin-static-resume-site/
