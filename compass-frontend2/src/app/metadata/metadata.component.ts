import { Component, OnInit } from '@angular/core';
import {Metadata} from "./metadata";
import {MetadataService} from "./metadata.service";
import {MetadataParameters} from "./metadata-parameters";
import {Router} from "@angular/router";

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
  ordering: string = null;
  showSpinner: boolean = true;
  // pagination settings
  private itemsPerPage: number = 10;
  maxSize: number = 5; // maxNumberButtonsVisible

  private params: MetadataParameters = new MetadataParameters();

  constructor(
    private metadataService: MetadataService,
    private router: Router
  ) {}

  ngOnInit() {
    this.getMostRecentMetadata();
    this.totalItems = 0;
  }

  private clearParams(): void {
    this.params.clear();
    this.ordering = null;
    this.params.page_size = this.itemsPerPage;
    this.params.language = this.language;
  }

  getMostRecentMetadata(): void {
    this.clearParams();
    this.params.ordering = '-modified';
    this.ordering = 'most recent first';
    this.getMetadataList();
  }

  filterMetadata(search): void {
    this.totalItems = 0;
    this.currentPage = 1;
    this.clearParams();
    this.params.page_size = this.itemsPerPage;
    this.params.ordering = 'rank';
    this.ordering = 'highest search rank first';
    this.params.search = search;
    this.params.language = this.language;
    this.getMetadataList();
  }

  languageChanged(language): void {
    this.language = language;
    this.params.language = this.language;
    if (this.params.search) {
      this.getMetadataList();
    }
  }

  gotoSingleEntry(metadata: Metadata): void {
    let link = ['/metadata', metadata.api_id];
    this.router.navigate(link);
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
