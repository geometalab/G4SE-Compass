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
  language: string = 'de';

  // pagination settings
  private itemsPerPage: number = 10;
  maxSize: number = 5; // maxNumberButtonsVisible

  private params: MetadataParameters = new MetadataParameters();

  constructor(private metadataService: MetadataService) {}

  ngOnInit() {
    this.getMostRecentMetadata();
    this.totalItems = 0;
  }

  private clearParams(): void {
    this.params.clear();
    this.params.page_size = this.itemsPerPage;
    this.params.language = this.language;
  }

  getMostRecentMetadata(): void {
    this.clearParams();
    // this.params.limit = 6;
    this.params.ordering = '-modified';
    this.getMetadataList();
  }

  filterMetadata(search): void {
    this.totalItems = 0;
    this.currentPage = 1;
    this.clearParams();
    this.params.page_size = this.itemsPerPage;
    this.params.ordering = '-rank';
    this.params.search = search;
    this.params.language = this.language;
    this.getMetadataList();
  }

  getAllMetadata(): void {
    this.clearParams();
    this.getMetadataList();
  }

  public pageChanged(event:any):void {
    this.params.page = event.page;
    this.getMetadataList();
  }

  private processData(metadata): void {
    this.metadataList = metadata.results;
    this.totalItems = metadata.count;
  }

  private getMetadataList(): void {
    this.metadataService
      .getMetadataList(this.params)
      .then(metadata => this.processData(metadata))
      .catch(error => this.error = error);
  }
}
