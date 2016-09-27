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
  totalItems:number = 0;
  currentPage:number = 1;
  private itemsPerPage: number = 10;

  private params: MetadataParameters = new MetadataParameters();

  constructor(private metadataService: MetadataService) {}

  ngOnInit() {
    this.getMostRecentMetadata();
    this.totalItems = 0;
  }

  getMostRecentMetadata(): void {
    this.params = new MetadataParameters();
    this.params.limit = 6;
    this.params.ordering = '-modified';
    this.getMetadataList();
  }

  filterMetadata(search): void {
    this.totalItems = 0;
    this.currentPage = 1;
    this.params = new MetadataParameters();
    this.params.page_size = this.itemsPerPage;
    this.params.ordering = '-modified';
    this.params.search = search;
    this.getMetadataList();
  }

  getAllMetadata(): void {
    this.params = new MetadataParameters();
    this.getMetadataList();
  }

  public pageChanged(event:any):void {
    this.params.page = event.page;
    console.log('Page changed to: ' + event.page);
    console.log('Number items per page: ' + event.itemsPerPage);
    this.getMetadataList();
  }

  private processData(metadata): void {
    this.metadataList = metadata.results;
    this.totalItems = metadata.count;
    // metadata => this.metadataList = metadata;
  }

  private getMetadataList(): void {
    this.metadataService
      .getMetadataList(this.params)
      .then(metadata => this.processData(metadata))
      .catch(error => this.error = error);
  }
}
