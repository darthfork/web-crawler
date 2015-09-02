require 'rubygems'
require 'mechanize'
require 'openssl'
def silence_warnings(&block)
  warn_level = $VERBOSE
  $VERBOSE = nil
  result = block.call
  $VERBOSE = warn_level
  result
end

silence_warnings do
  I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil
  OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
end

class OlaCrawler
  def self.crawl(cityid, pickupdate, pickuptime)
    @agent = Mechanize.new { |a|
      a.user_agent_alias = 'Mac Safari'
    }
    @agent.get('https://olacabs.com') do |page|
      @search_result = page.form_with(:id => 'search_form') do |search|
        search.cityID = cityid
        search.pickupDate = pickupdate #Format - 'dd/mm/yyyy'
        search.pickupTime = pickuptime #Format - 'hh:mm AM/PM'
      end.submit
      @crawl_output = Hash.new
      @booking_details = @search_result.at("#bookingDetailsTable")
      @booking_info = @search_result.at('.bookinginfo-content')
      
      @crawl_output.merge!("Car Category: " => @booking_details.at('tr[1]').at('.descValue').text.strip)
      @crawl_output.merge!("Location: " => @booking_details.at('tr[2]').at('.descValue').text.strip)
      @crawl_output.merge!("Usage: " => @booking_details.at('tr[3]').at('.descValue').text.strip)
      @crawl_output.merge!("Pickup Date: " => @booking_details.at('tr[4]').at('.descValue').text.strip)
      @crawl_output.merge!("Pickup Time: " => @booking_details.at('tr[5]').at('.descValue').text.strip)
      @crawl_output.merge!("Minimum Bill of: Rs." => @booking_info.at('#baseFare').text.strip)
      @crawl_output.merge!("Per KM charge: Rs." => @booking_info.at('#perKm').text.strip)
      @crawl_output.merge!("Per Minute: " => @booking_info.at('#perMin').text.strip )
      @crawl_output.merge!("Service Tax: " => @booking_info.at('#serviceTax').text.strip)
      @crawl_output.merge!("Wait Time Charge: " => @booking_info.at('.wait-time-chargable-text').text.strip)
      return @crawl_output 
    end
  end
end

begin
    OlaCrawler.crawl('1','31/07/2015','01:00 PM').each do |k,v| # '1' is for Mumbai
        puts k + " " + v
    end
end
