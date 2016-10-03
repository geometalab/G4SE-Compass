import { CompassFrontend2Page } from './app.po';

describe('compass-frontend2 App', function() {
  let page: CompassFrontend2Page;

  beforeEach(() => {
    page = new CompassFrontend2Page();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
