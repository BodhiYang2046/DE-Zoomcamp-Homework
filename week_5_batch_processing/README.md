gcloud components update

gsutil -m cp -r fhv gs://de-zoomcamp-homework5-batch-bodhi-yang 

gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar gcs-connector-hadoop3-2.2.5.jar  


./sbin/start-master.sh


./sbin/start-worker.sh spark://BodhitekiMBP.lan:7077

./sbin/stop-all.sh