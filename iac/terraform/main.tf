resource "kubernetes_pod" "smartirrigation" {
  metadata {
    name = "smartirrigation"
    namespace = "evolved5g"
    labels = {
      app = "smartirrigation"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/dummy-netapp:latest"
      name  = "dummy-netapp"
    }
  }
}

resource "kubernetes_service" "smartirrigation_service" {
  metadata {
    name = "smartirrigation"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.smartirrigation.metadata.0.labels.app
    }
    port {
      port = 8000
      target_port = 8000
    }
  }
}
