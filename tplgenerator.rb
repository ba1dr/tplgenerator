#!/usr/bin/env ruby
# encoding: utf-8

_fdescr = <<EODESC
    Generate project from the template

    Author: Alexey Kolyanov, 2015
EODESC

require 'rubygems'
require 'optparse'
require 'fileutils'
require 'yaml'
require 'erubis'

tplname = nil
appname = nil
create_dir = nil
workdir = nil
$debugmode = false
$quiet = false

# get command-line parameters
OptionParser.new do |opts|
    opts.banner = "Usage: ruby #{__FILE__} [options]"

    opts.on('-t', '--template tplname', 'Template Name') { |v| tplname = v }
    opts.on('-a', '--appname appname', 'App Name') { |v| appname = v }
    opts.on('-d', '--dir', 'Create dir with appname (defaults to template''s settings)') { |v| create_dir = true }
    opts.on('-D', '--no-dir', 'Do not create dir with appname') { |v| create_dir = false }
    opts.on('-p', '--path PATH', 'Root path to the project') { |v| workdir = v }
    opts.on('-X', '--debug', 'Enable debug mode') { $debugmode = true }
    opts.on('-q', '--quiet', 'Disable output') { $quiet = true }

end.parse!

# ARGV.shift  # 0
arg1 = ARGV.shift
tplname = arg1 if arg1
arg1 = ARGV.shift
appname = arg1 if arg1


module TplGenerator; class << self
    CURDIR = Dir.getwd
    APPDIR = File.dirname(File.expand_path(__FILE__))
    TPLDIR = File.join(APPDIR, "templates")

    def get_tplist
        retval = []
        Dir.glob("#{TPLDIR}/*/meta.yaml").each do |mf|
            item = {metafile: mf, dir: File.dirname(mf), ignore_files: ['meta.yaml']}
            idata = YAML.load_file(mf)
            item.update(idata)
            retval << item
        end
        retval
    end

    def generate(tp, proj_name, create_dir: nil, workdir: nil)
        tpdlen = tp[:dir].length + 1
        proj_dir = (workdir or CURDIR)
        create_dir = tp[:create_dir] if create_dir.nil?
        create_dir = true if create_dir.nil?  # default
        if create_dir
            proj_dir = File.join(proj_dir, proj_name)
            FileUtils.mkdir_p(proj_dir)
            puts "Created project directory: #{proj_dir}"
        end
        Dir.glob("#{tp[:dir]}/**/*", File::FNM_DOTMATCH).each do |fulltppath|
            relpath = fulltppath[tpdlen, 1000]
            next if relpath == '.' or relpath == '.' or relpath.start_with? '.git/' or relpath.start_with? '.svn/'
            next if tp[:ignore_files].detect {|ff| ff == relpath}
            newpath = File.join(proj_dir, relpath)
            if File.directory? fulltppath
                FileUtils.mkdir_p(newpath)
                puts "Created directory #{newpath}"
                next
            elsif relpath.end_with? '.erb'
                newpath[-4, 4] = ''
                context = {
                    project_name: proj_name, context: tp[:context]
                }
                fdata = ""
                File.open(fulltppath, "r:UTF-8") { |f| fdata = f.read() }
                erb_templ = Erubis::Eruby.new(fdata)
                result = erb_templ.evaluate(context)
                File.open(newpath, 'w:UTF-8') { |f| f.write(result) }
                puts "Generated template #{relpath}"
            else
                FileUtils.cp(fulltppath, newpath)
                puts "Copied file #{relpath}"
            end
        end
    end

    def main(tpname: nil, appname: nil, create_dir: nil, workdir: nil)
        if not appname
            puts "ERROR: Application name should be passed!"
            return false
        end
        tplist = get_tplist
        # tpname = 'ruby'
        tp = tplist.find {|xt| xt['aliases'].detect {|a| a.downcase == tpname } }
        if tp
            generate(tp, appname, create_dir: create_dir, workdir: workdir)
        else
            puts "ERROR: template not found for #{tpname}"
        end
    end

end; end  # module TplGenerator

TplGenerator::main(tpname: tplname, appname: appname, create_dir: create_dir, workdir: workdir)
