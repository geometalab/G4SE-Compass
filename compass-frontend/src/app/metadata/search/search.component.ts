import { Component, OnInit } from '@angular/core';
import {SearchResult} from "./search-result";
import {Router} from "@angular/router";
import {SearchParameters} from "./search-parameters";
import {SearchService} from "./search.service";


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
})
export class SearchComponent implements OnInit {
  searchResultList: SearchResult[];
  error: any;
  totalItems:number = 0;
  currentPage:number = 1;
  isLoading: boolean = false;
  // pagination settings
  private itemsPerPage: number = 10;
  maxSize: number = 5; // maxNumberButtonsVisible

  private searchParams: SearchParameters = new SearchParameters();

  constructor(
    private searchService: SearchService,
    private router: Router
  ) { }

  ngOnInit() {
    this.searchParams.language = 'de';
    this.searchParams.page = 1;
    this.searchParams.page_size = this.itemsPerPage;
    this.executeSearch();
  }

  executeSearch(): void {
    this.searchResultList = [];
    this.searchParams.page = 1;
    this.getMetadataList();
  }

  languageChanged(): void {
    this.getMetadataList();
  }

  pageChanged(event:any): void {
    this.searchParams.page = event.page;
    this.getMetadataList();
  }

  private loading(): void {
    this.searchParams.loading = true;
  }

  private loadingFinished(): void {
    this.searchParams.loading = false;
  }

  private processData(searchResults): void {
    this.searchResultList = searchResults.results;
    this.totalItems = searchResults.count;
    this.loadingFinished();
  }

  private processError(error): void {
    console.log(error);
    this.loadingFinished();
  }

  private getMetadataList(): void {
    this.loading();
    this.searchService
      .getSearchResultList(this.searchParams)
      .then(searchResults => this.processData(searchResults))
      .catch(error => this.processError(error));
  }


}
