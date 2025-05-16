#!/usr/bin/env ruby

line = ARGV[0]

if line =~ /\[from:([^\]]+)\].*\[to:([^\]]+)\].*\[flags:([^\]]+)\]/
  sender = $1
  receiver = $2
  flags = $3
  puts "#{sender},#{receiver},#{flags}"
end

