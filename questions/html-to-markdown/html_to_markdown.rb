require 'nokogiri'

def html_to_markdown(html)
  doc = Nokogiri::HTML(html)
  
  doc.css('script, style').each { |node| node.remove }
  
  doc.css('h1').each { |node| node.content = "# #{node.content}" }
  doc.css('h2').each { |node| node.content = "## #{node.content}" }
  doc.css('h3').each { |node| node.content = "### #{node.content}" }
  doc.css('h4').each { |node| node.content = "#### #{node.content}" }
  doc.css('h5').each { |node| node.content = "##### #{node.content}" }
  doc.css('h6').each { |node| node.content = "###### #{node.content}" }
  
  doc.css('strong, b').each { |node| node.content = "**#{node.content}**" }
  doc.css('em, i').each { |node| node.content = "*#{node.content}*" }
  
  doc.css('a').each do |node|
    href = node['href']
    text = node.content
    node.replace("[#{text}](#{href})")
  end
  
  doc.css('img').each do |node|
    src = node['src']
    alt = node['alt'] || ''
    node.replace("![#{alt}](#{src})")
  end
  
  doc.css('ul, ol').each do |list|
    list.css('li').each do |item|
      prefix = list.name == 'ol' ? "1. " : "- "
      item.content = prefix + item.content
    end
  end
  
  doc.css('blockquote').each { |node| node.content = "> #{node.content}" }
  
  doc.css('code').each { |node| node.content = "`#{node.content}`" }
  doc.css('pre').each { |node| node.content = "```\n#{node.content}\n```" }
  
  text = doc.text.gsub(/\s+/, ' ').strip
  
  text.gsub(/\n{3,}/, "\n\n")
end