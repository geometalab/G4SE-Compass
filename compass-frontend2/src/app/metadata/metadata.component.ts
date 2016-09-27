import { Component, OnInit } from '@angular/core';
import {Metadata} from "./metadata";
import {MetadataService} from "./metadata.service";
import {MetadataParameters} from "./metadata-parameters";

@Component({
  selector: 'app-metadata',
  templateUrl: './metadata.component.html',
  styleUrls: ['./metadata.component.css']
})
export class MetadataComponent implements OnInit {
  metadataList: Metadata[];
  error: any;
  params: MetadataParameters = new MetadataParameters();

  constructor(private metadataService: MetadataService) {}

  ngOnInit() {
    this.getMostRecent();
  }

  getMostRecent(): void {
    this.params = new MetadataParameters();
    this.params.limit = 6;
    this.params.ordering = '-modified';
    this.getMetadataList();
  }

  private getMetadataList(): void {
    this.metadataService
      .getMetadataList(this.params)
      .then(metadata => this.metadataList = metadata)
      .catch(error => this.error = error);
  }
}
