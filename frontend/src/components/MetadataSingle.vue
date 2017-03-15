<template>
  <div>
    <loading v-if="loading"></loading>
    <div v-else>
      <div v-if="this.error" class="alert-danger">
        {{this.error}}
      </div>
      <div v-else>
        <span v-if="metadataItem.title">
          <h4>Title</h4>
          <p>{{metadataItem.title}}</p>
        </span>
        <span v-if="metadataItem.abstract">
          <h4>Abstract</h4>
          <p>{{metadataItem.abstract}}</p>
        </span>
        <span v-if="metadataItem.publication_year">
          <h4>Publication Year</h4>
          <p>{{metadataItem.publication_year}}</p>
        </span>
        <span v-if="metadataItem.publication_lineage">
          <h4>Publication Lineage</h4>
          <p>{{metadataItem.publication_lineage}}</p>
        </span>
        <span v-if="metadataItem.is_latest">
          <h4>Latest in series</h4>
          <p>{{metadataItem.is_latest | truthiness}}</p>
        </span>
        <span v-if="metadataItem.geography">
          <h4>Geography</h4>
          <p>{{metadataItem.geography}}</p>
        </span>
        <span v-if="metadataItem.geodata_type">
          <h4>Geodata Type</h4>
          <p>{{metadataItem.geodata_type}}</p>
        </span>
        <span v-if="metadataItem.source">
          <h4>Source</h4>
          <p>{{metadataItem.source}}</p>
        </span>
        <span v-if="metadataItem.metadata_link">
          <h4>Metadata Link</h4>
          <p>{{metadataItem.metadata_link}}</p>
        </span>
        <span v-if="metadataItem.access_link">
          <h4>Access Link</h4>
          <p>{{metadataItem.access_link}}</p>
        </span>
        <span v-if="metadataItem.base_link">
          <h4>Base Link</h4>
          <p>{{metadataItem.base_link}}</p>
        </span>
        <span v-if="metadataItem.collection">
          <h4>Collection</h4>
          <p>{{metadataItem.collection}}</p>
        </span>
        <span v-if="metadataItem.dataset">
          <h4>Dataset</h4>
          <p>{{metadataItem.dataset}}</p>
        </span>
        <span v-if="metadataItem.arcgis_layer_link">
          <h4>ArcGIS Layer Link</h4>
          <p>{{metadataItem.arcgis_layer_link}}</p>
        </span>
        <span v-if="metadataItem.qgis_layer_link">
          <h4>QGIS Layer Link</h4>
          <p>{{metadataItem.qgis_layer_link}}</p>
        </span>
        <span v-if="metadataItem.arcgis_symbology_link">
          <h4>ArcGIS Symbology Link</h4>
          <p>{{metadataItem.arcgis_symbology_link}}</p>
        </span>
        <span v-if="metadataItem.qgis_symbology_link">
          <h4>QGIS Symbology Link</h4>
          <p>{{metadataItem.qgis_symbology_link}}</p>
        </span>
        <span v-if="metadataItem.service_type">
          <h4>Service Type</h4>
          <p>{{metadataItem.service_type}}</p>
        </span>
        <span v-if="metadataItem.crs">
          <h4>CRS (Coordinate Reference System)</h4>
          <p>{{metadataItem.crs}}</p>
        </span>
        <span v-if="metadataItem.term_link">
          <h4>Terms of Use</h4>
          <p>{{metadataItem.term_link}}</p>
        </span>
        <span v-if="metadataItem.modified">
          <h4>Last Modification</h4>
          <p>{{metadataItem.modified | dateify}}</p>
        </span>
      </div>
    </div>
  </div>
</template>
<script>
  import PulseLoader from 'vue-spinner/src/PulseLoader';

  export default {
    name: 'metadata-single',
    props: {
      id: {
        type: String,
        required: true,
      },
    },
    created() {
      this.getItem();
    },
    data() {
      return {
        metadataItem: null,
        loading: false,
        error: null,
      };
    },
    components: {
      loading: PulseLoader,
    },
    methods: {
      getItem() {
        this.loading = true;
        this.$http.get(`/api/metadata/${this.id}/`).then((response) => {
          this.metadataItem = response.body;
          this.error = null;
        }, (response) => {
          this.error = response.body.detail;
          this.metadataItem = null;
        }).then(() => {
          this.loading = false;
        });
      },
    },
    filters: {
      truthiness(value) {
        if (value) {
          return 'Yes';
        }
        return 'No';
      },
      dateify(value) {
        return new Date(value).toLocaleDateString();
      },
    },
  };
</script>
