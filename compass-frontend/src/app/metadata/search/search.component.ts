import { Component, OnInit } from '@angular/core';
import {SearchResult} from "./search-result";
import {Router} from "@angular/router";
import {SearchParameters} from "./search-parameters";
import {SearchService} from "./search.service";
import {SearchStore} from "./search.store";


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
})
export class SearchComponent implements OnInit {
  error: any;
  // pagination settings
  private itemsPerPage: number = 10;
  maxSize: number = 5; // maxNumberButtonsVisible

  private searchParams: SearchParameters = new SearchParameters();

  constructor(
    private searchStore: SearchStore,
    private router: Router
  ) { }

  ngOnInit() {
    this.searchParams.language = 'de';
    this.searchParams.page = 1;
    this.searchParams.page_size = this.itemsPerPage;
    this.executeSearch(null);
  }

  executeSearch(event:any): void {
    this.searchParams.page = 1;
    this.getMetadataList();
  }

  pageChanged(event:any): void {
    this.searchParams.page = event.page;
    this.getMetadataList();
  }

  private getMetadataList(): void {
    this.searchStore.search(this.searchParams);
  }


}
