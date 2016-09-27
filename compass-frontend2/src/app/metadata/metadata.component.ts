import { Component, OnInit } from '@angular/core';
import {Metadata} from "./metadata";
import {MetadataService} from "./metadata.service";

@Component({
  selector: 'app-metadata',
  templateUrl: './metadata.component.html',
  styleUrls: ['./metadata.component.css']
})
export class MetadataComponent implements OnInit {
  metadataList: Metadata[];
  selectedMetadata: Metadata;
  error: any;

  constructor(private metadataService: MetadataService) { }

  ngOnInit() {
    this.getMetadataList();
  }

  getMetadataList(): void {
    this.metadataService
      .getMetadataList()
      .then(metadata => this.metadataList = metadata)
      .catch(error => this.error = error);
  }
}
