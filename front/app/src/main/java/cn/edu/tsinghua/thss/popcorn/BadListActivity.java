package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import cn.edu.tsinghua.thss.popcorn.bean.RepairRecordBean;
import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.JsonUtil;
import cn.edu.tsinghua.thss.popcorn.utils.SharedPreferencesUtil;

public class BadListActivity extends Activity {

    ProgressDialog progressDialog;
    private String[] mBrief, mName, mFormContent, mFormId;
    private TableListAdapter mAdapter;
    private String mRouteId;
    private static int REQUEST_CODE = 2, ONE_SUBMIT_FINISHED = 3;
    private ListView myListView;
    private Button submitBtn;
    private int completedForm;
    private int oneSubmitMessage = 0;
    private SharedPreferences sp;
    private ArrayList<RepairRecordBean.Info> recordList=new ArrayList<RepairRecordBean.Info>();
    private TableListAdapter adapter;
    private RepairRecordBean repairRecordBean;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bad_list);
        myListView = (ListView) findViewById(R.id.badlist_listview);
        myListView.setDivider(null);//去除listview的下划线
        initData();

        myListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapter, View view, int position,
                                    long id) {
                //进入报警详情页面，如果已读，设置背景颜色为灰色
                Intent intent = new Intent(BadListActivity.this, BadItemActivity.class);

                intent.putExtra("info", recordList.get(position));
                BadListActivity.this.startActivity(intent);


            }

        });

    }

    /**
     * 初始化数据
     */
    private void initData() {
//        Log.e("result==========","=============="+11);
        getData(Config.REPAIR_BAD);
//        getData(Config.REPAIR_TASK_LIST_URL);
    }

    /**
     * 获取网络数据
     */
    private void getData(String url) {
        HttpUtils httpUtils=new HttpUtils();

        RequestParams params=new RequestParams();
        params.addQueryStringParameter("username",Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token",Config.ACCESS_TOKEN);
        /*params.addQueryStringParameter("start_date",SharedPreferencesUtil.getString(this,Config.START_DAY,null));
        params.addQueryStringParameter("end_date",SharedPreferencesUtil.getString(this,Config.END_DAY,null));*/

        httpUtils.send(HttpRequest.HttpMethod.GET, url, params,new RequestCallBack<String>() {
            @Override
            public void onSuccess(ResponseInfo<String> responseInfo) {
                String json = responseInfo.result;
//                SharedPreferencesUtil.putString(BadListActivity.this,Config.REPAIR_RECORD_JSON,json);
//                Log.e("result++++++++++","=============="+json);
                processJson(json);
            }

            @Override
            public void onFailure(HttpException error, String msg) {
                Log.e("error++++++++++","=============="+msg);
            }
        });
    }

    /**
     * 解析json
     * @param json
     */
    private void processJson(String json) {
        repairRecordBean = JsonUtil.json2Bean(json, RepairRecordBean.class);
        if (repairRecordBean.data.size() > 0){
            recordList.addAll(repairRecordBean.data);
        }
        if(adapter==null){
            adapter = new TableListAdapter();
            myListView.setAdapter(adapter);
        }else {
            adapter.notifyDataSetChanged();
        }
    }

    /**
     * 适配
     */
    class TableListAdapter extends BaseAdapter{
        ViewHolder vh;
        @Override
        public int getCount() {
            return recordList.size();
        }

        @Override
        public RepairRecordBean.Info getItem(int position) {
            return recordList.get(position);
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if(convertView==null){
                vh=new ViewHolder();
                convertView = View.inflate(BadListActivity.this, R.layout.list_rell_bad, null);
                vh.title = (TextView) convertView.findViewById(R.id.tv_title);
                vh.description = (TextView) convertView.findViewById(R.id.tv_desc);
                vh.time = (TextView) convertView.findViewById(R.id.tv_time);
                vh.commentCount = (TextView) convertView.findViewById(R.id.tv_comment_count);
                convertView.setTag(vh);
            }else{
                vh= (ViewHolder) convertView.getTag();
            }
            vh.title.setText(getItem(position).memo);
            vh.description.setText(getItem(position).description);
            vh.time.setText(getItem(position).create_time);
            vh.commentCount.setText(getItem(position).id+"");
            return convertView;
        }
    }
    class ViewHolder{
        TextView title;
        TextView description;
        TextView time;
        TextView commentCount;
    }
}