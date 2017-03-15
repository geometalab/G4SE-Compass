<template>
  <div class="col-md-12">
    <loading v-if="loading"></loading>
    <div v-else>
      <div v-if="this.error" class="alert-danger">
        {{this.error}}
      </div>
      <div v-else>
        <h3>{{metadataItem.title}} ({{metadataItem.id}})</h3>
        <span v-if="metadataItem.title">
          <h5>Title</h5>
          <p>{{metadataItem.title}}</p>
        </span>
        <span v-if="metadataItem.abstract">
          <h5>Abstract</h5>
          <p>{{metadataItem.abstract}}</p>
        </span>
        <span v-if="metadataItem.publication_year">
          <h5>Publication Year</h5>
          <p>{{metadataItem.publication_year}}</p>
        </span>
        <span v-if="metadataItem.publication_lineage">
          <h5>Publication Lineage</h5>
          <p>{{metadataItem.publication_lineage}}</p>
        </span>
        <span v-if="metadataItem.is_latest">
          <h5>Latest in series</h5>
          <p>{{metadataItem.is_latest | truthiness}}</p>
        </span>
        <span v-if="metadataItem.geography">
          <h5>Geography</h5>
          <p>{{metadataItem.geography}}</p>
        </span>
        <span v-if="metadataItem.geodata_type">
          <h5>Geodata Type</h5>
          <p>{{metadataItem.geodata_type}}</p>
        </span>
        <span v-if="metadataItem.source">
          <h5>Source</h5>
          <p>{{metadataItem.source}}</p>
        </span>
        <span v-if="metadataItem.metadata_link">
          <h5>Metadata Link</h5>
          <generated-link :url="metadataItem.metadata_link"></generated-link>
        </span>
        <span v-if="metadataItem.access_link">
          <h5>Access Link</h5>
          <generated-link :url="metadataItem.access_link"></generated-link>
        </span>
        <span v-if="metadataItem.base_link">
          <h5>Base Link</h5>
          <generated-link :url="metadataItem.base_link"></generated-link>
        </span>
        <span v-if="metadataItem.collection">
          <h5>Collection</h5>
          <p>{{metadataItem.collection}}</p>
        </span>
        <span v-if="metadataItem.dataset">
          <h5>Dataset</h5>
          <p>{{metadataItem.dataset}}</p>
        </span>
        <span v-if="metadataItem.arcgis_layer_link">
          <h5>ArcGIS Layer Link</h5>
          <generated-link :url="metadataItem.arcgis_layer_link"></generated-link>
        </span>
        <span v-if="metadataItem.qgis_layer_link">
          <h5>QGIS Layer Link</h5>
          <generated-link :url="metadataItem.qgis_layer_link"></generated-link>
        </span>
        <span v-if="metadataItem.arcgis_symbology_link">
          <h5>ArcGIS Symbology Link</h5>
          <generated-link :url="metadataItem.arcgis_symbology_link"></generated-link>
        </span>
        <span v-if="metadataItem.qgis_symbology_link">
          <h5>QGIS Symbology Link</h5>
          <generated-link :url="metadataItem.qgis_symbology_link"></generated-link>
        </span>
        <span v-if="metadataItem.service_type">
          <h5>Service Type</h5>
          <p>{{metadataItem.service_type}}</p>
        </span>
        <span v-if="metadataItem.crs">
          <h5>CRS (Coordinate Reference System)</h5>
          <p>{{metadataItem.crs}}</p>
        </span>
        <span v-if="metadataItem.term_link">
          <h5>Terms of Use</h5>
          <generated-link :url="metadataItem.term_link"></generated-link>
        </span>
        <span v-if="metadataItem.modified">
          <h5>Last Modification</h5>
          <p>{{metadataItem.modified | dateify}}</p>
        </span>
      </div>
    </div>
  </div>
</template>
<script>
  import PulseLoader from 'vue-spinner/src/PulseLoader';
  import GeneratedLink from './GeneratedLink';

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
      'generated-link': GeneratedLink,
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
      linkify(value) {
        return `<a href="${value}">${value}</a>`;
      },
    },
  };
</script>
